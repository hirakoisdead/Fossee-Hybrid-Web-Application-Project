import io
import pandas as pd
from django.http import HttpResponse
from django.db.models import Count
from django.contrib.auth.models import User
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

from .models import EquipmentDataset, Equipment
from .serializers import (
    UserSerializer, 
    EquipmentDatasetListSerializer,
    EquipmentDatasetDetailSerializer,
    DatasetSummarySerializer
)


class RegisterView(generics.CreateAPIView):
    """User registration endpoint."""
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """User login endpoint."""
    from django.contrib.auth import authenticate
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Please provide both username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        })
    
    return Response(
        {'error': 'Invalid credentials'},
        status=status.HTTP_401_UNAUTHORIZED
    )


class CSVUploadView(APIView):
    """Handle CSV file upload and parsing."""
    parser_classes = [MultiPartParser]
    
    def post(self, request):
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        csv_file = request.FILES['file']
        
        if not csv_file.name.endswith('.csv'):
            return Response(
                {'error': 'File must be a CSV'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Read CSV with pandas
            df = pd.read_csv(csv_file)
            
            # Validate required columns
            required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return Response(
                    {'error': f'Missing columns: {", ".join(missing_columns)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Calculate summary statistics
            total_count = len(df)
            avg_flowrate = round(df['Flowrate'].mean(), 2)
            avg_pressure = round(df['Pressure'].mean(), 2)
            avg_temperature = round(df['Temperature'].mean(), 2)
            
            # Create dataset
            dataset = EquipmentDataset.objects.create(
                user=request.user,
                filename=csv_file.name,
                total_count=total_count,
                avg_flowrate=avg_flowrate,
                avg_pressure=avg_pressure,
                avg_temperature=avg_temperature
            )
            
            # Create equipment records
            equipment_records = []
            for _, row in df.iterrows():
                equipment_records.append(Equipment(
                    dataset=dataset,
                    name=row['Equipment Name'],
                    equipment_type=row['Type'],
                    flowrate=row['Flowrate'],
                    pressure=row['Pressure'],
                    temperature=row['Temperature']
                ))
            Equipment.objects.bulk_create(equipment_records)
            
            # Enforce 5 dataset limit per user
            user_datasets = EquipmentDataset.objects.filter(user=request.user).order_by('-uploaded_at')
            if user_datasets.count() > 5:
                datasets_to_delete = user_datasets[5:]
                for ds in datasets_to_delete:
                    ds.delete()
            
            return Response(
                EquipmentDatasetDetailSerializer(dataset).data,
                status=status.HTTP_201_CREATED
            )
            
        except pd.errors.EmptyDataError:
            return Response(
                {'error': 'CSV file is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class DatasetListView(generics.ListAPIView):
    """List user's datasets (last 5)."""
    serializer_class = EquipmentDatasetListSerializer
    
    def get_queryset(self):
        return EquipmentDataset.objects.filter(user=self.request.user)[:5]


class DatasetDetailView(generics.RetrieveDestroyAPIView):
    """Get or delete a specific dataset."""
    serializer_class = EquipmentDatasetDetailSerializer
    
    def get_queryset(self):
        return EquipmentDataset.objects.filter(user=self.request.user)


class DatasetSummaryView(APIView):
    """Get detailed summary statistics for a dataset."""
    
    def get(self, request, pk):
        try:
            dataset = EquipmentDataset.objects.get(pk=pk, user=request.user)
        except EquipmentDataset.DoesNotExist:
            return Response(
                {'error': 'Dataset not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        equipment = dataset.equipment_items.all()
        
        # Type distribution
        type_counts = equipment.values('equipment_type').annotate(count=Count('id'))
        type_distribution = {item['equipment_type']: item['count'] for item in type_counts}
        
        # Min/Max values
        if equipment.exists():
            min_values = {
                'flowrate': round(min(e.flowrate for e in equipment), 2),
                'pressure': round(min(e.pressure for e in equipment), 2),
                'temperature': round(min(e.temperature for e in equipment), 2)
            }
            max_values = {
                'flowrate': round(max(e.flowrate for e in equipment), 2),
                'pressure': round(max(e.pressure for e in equipment), 2),
                'temperature': round(max(e.temperature for e in equipment), 2)
            }
        else:
            min_values = max_values = {'flowrate': 0, 'pressure': 0, 'temperature': 0}
        
        summary = {
            'total_count': dataset.total_count,
            'avg_flowrate': dataset.avg_flowrate,
            'avg_pressure': dataset.avg_pressure,
            'avg_temperature': dataset.avg_temperature,
            'type_distribution': type_distribution,
            'min_values': min_values,
            'max_values': max_values
        }
        
        return Response(DatasetSummarySerializer(summary).data)


class GeneratePDFReportView(APIView):
    """Generate PDF report for a dataset."""
    
    def get(self, request, pk):
        try:
            dataset = EquipmentDataset.objects.get(pk=pk, user=request.user)
        except EquipmentDataset.DoesNotExist:
            return Response(
                {'error': 'Dataset not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Create PDF in memory
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=72)
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1
        )
        elements.append(Paragraph("Equipment Analysis Report", title_style))
        elements.append(Spacer(1, 12))
        
        # Dataset info
        info_style = styles['Normal']
        elements.append(Paragraph(f"<b>File:</b> {dataset.filename}", info_style))
        elements.append(Paragraph(f"<b>Uploaded:</b> {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M')}", info_style))
        elements.append(Paragraph(f"<b>Total Equipment:</b> {dataset.total_count}", info_style))
        elements.append(Spacer(1, 20))
        
        # Summary statistics
        elements.append(Paragraph("Summary Statistics", styles['Heading2']))
        elements.append(Spacer(1, 10))
        
        summary_data = [
            ['Metric', 'Average', 'Min', 'Max'],
        ]
        
        equipment = list(dataset.equipment_items.all())
        if equipment:
            flowrates = [e.flowrate for e in equipment]
            pressures = [e.pressure for e in equipment]
            temperatures = [e.temperature for e in equipment]
            
            summary_data.extend([
                ['Flowrate', f'{dataset.avg_flowrate:.2f}', f'{min(flowrates):.2f}', f'{max(flowrates):.2f}'],
                ['Pressure', f'{dataset.avg_pressure:.2f}', f'{min(pressures):.2f}', f'{max(pressures):.2f}'],
                ['Temperature', f'{dataset.avg_temperature:.2f}', f'{min(temperatures):.2f}', f'{max(temperatures):.2f}']
            ])
        
        summary_table = Table(summary_data, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0'))
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
        
        # Equipment type distribution
        elements.append(Paragraph("Equipment Type Distribution", styles['Heading2']))
        elements.append(Spacer(1, 10))
        
        type_counts = {}
        for eq in equipment:
            type_counts[eq.equipment_type] = type_counts.get(eq.equipment_type, 0) + 1
        
        type_data = [['Equipment Type', 'Count', 'Percentage']]
        for eq_type, count in sorted(type_counts.items()):
            percentage = (count / len(equipment) * 100) if equipment else 0
            type_data.append([eq_type, str(count), f'{percentage:.1f}%'])
        
        type_table = Table(type_data, colWidths=[2.5*inch, 1.2*inch, 1.2*inch])
        type_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0'))
        ]))
        elements.append(type_table)
        elements.append(Spacer(1, 20))
        
        # Equipment list
        elements.append(Paragraph("Equipment List", styles['Heading2']))
        elements.append(Spacer(1, 10))
        
        eq_data = [['Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']]
        for eq in equipment[:50]:  # Limit to first 50 for PDF
            eq_data.append([
                eq.name, eq.equipment_type, 
                f'{eq.flowrate:.1f}', f'{eq.pressure:.1f}', f'{eq.temperature:.1f}'
            ])
        
        eq_table = Table(eq_data, colWidths=[1.4*inch, 1.2*inch, 0.9*inch, 0.9*inch, 1*inch])
        eq_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0'))
        ]))
        elements.append(eq_table)
        
        doc.build(elements)
        
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="equipment_report_{dataset.id}.pdf"'
        
        return response
