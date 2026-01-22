# companies/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .models import Company, Internship
from .serializers import CompanySerializer, InternshipListSerializer, InternshipDetailSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def company_list(request):
    """
    Get list of all approved companies
    Supports search by name, industry, or description
    """
    companies = Company.objects.filter(is_approved=True)
    
    # Search functionality
    search = request.query_params.get('search', None)
    if search:
        companies = companies.filter(
            company_name__icontains=search
        ) | companies.filter(
            industry__icontains=search
        ) | companies.filter(
            description__icontains=search
        )
    
    # Ordering
    ordering = request.query_params.get('ordering', '-created_at')
    companies = companies.order_by(ordering)
    
    # Pagination
    page_number = request.query_params.get('page', 1)
    page_size = request.query_params.get('page_size', 10)
    paginator = Paginator(companies, page_size)
    page_obj = paginator.get_page(page_number)
    
    serializer = CompanySerializer(page_obj, many=True)
    
    return Response({
        'count': paginator.count,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'results': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def company_detail(request, pk):
    """
    Get details of a specific company
    """
    company = get_object_or_404(Company, pk=pk, is_approved=True)
    serializer = CompanySerializer(company)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def internship_list(request):
    """
    Get list of all active internships/attachments
    Supports filtering and searching
    """
    internships = Internship.objects.filter(
        is_active=True, 
        company__is_approved=True
    ).select_related('company')
    
    # Filter by placement type
    placement_type = request.query_params.get('placement_type', None)
    if placement_type:
        internships = internships.filter(placement_type=placement_type)
    
    # Filter by company
    company_id = request.query_params.get('company', None)
    if company_id:
        internships = internships.filter(company_id=company_id)
    
    # Filter by location
    location = request.query_params.get('location', None)
    if location:
        internships = internships.filter(location__icontains=location)
    
    # Search functionality
    search = request.query_params.get('search', None)
    if search:
        internships = internships.filter(
            title__icontains=search
        ) | internships.filter(
            description__icontains=search
        ) | internships.filter(
            requirements__icontains=search
        ) | internships.filter(
            company__company_name__icontains=search
        )
    
    # Ordering
    ordering = request.query_params.get('ordering', 'application_deadline')
    internships = internships.order_by(ordering)
    
    # Pagination
    page_number = request.query_params.get('page', 1)
    page_size = request.query_params.get('page_size', 10)
    paginator = Paginator(internships, page_size)
    page_obj = paginator.get_page(page_number)
    
    serializer = InternshipListSerializer(page_obj, many=True)
    
    return Response({
        'count': paginator.count,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'results': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def internship_detail(request, pk):
    """
    Get detailed information about a specific internship
    """
    internship = get_object_or_404(
        Internship, 
        pk=pk, 
        is_active=True, 
        company__is_approved=True
    )
    serializer = InternshipDetailSerializer(internship)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def internship_by_company(request):
    """
    Get internships filtered by company
    """
    company_id = request.query_params.get('company_id')
    
    if not company_id:
        return Response(
            {'error': 'company_id parameter is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    internships = Internship.objects.filter(
        company_id=company_id,
        is_active=True,
        company__is_approved=True
    )
    
    serializer = InternshipListSerializer(internships, many=True)
    return Response(serializer.data)


# applications/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Application
from .serializers import (
    ApplicationCreateSerializer,
    ApplicationListSerializer,
    ApplicationDetailSerializer
)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def application_list_create(request):
    """
    GET: List all applications for the current student
    POST: Create a new application
    """
    # Check if user has a student profile
    if not hasattr(request.user, 'student'):
        return Response(
            {'error': 'Only students can access applications'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    student = request.user.student
    
    if request.method == 'GET':
        applications = Application.objects.filter(student=student)
        
        # Filter by status
        status_filter = request.query_params.get('status', None)
        if status_filter:
            applications = applications.filter(status=status_filter)
        
        # Filter by admin approval
        admin_approved = request.query_params.get('admin_approved', None)
        if admin_approved is not None:
            applications = applications.filter(
                admin_approved=admin_approved.lower() == 'true'
            )
        
        # Ordering
        applications = applications.order_by('-applied_at')
        
        # Pagination
        page_number = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 10)
        paginator = Paginator(applications, page_size)
        page_obj = paginator.get_page(page_number)
        
        serializer = ApplicationListSerializer(page_obj, many=True)
        
        return Response({
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'current_page': page_obj.number,
            'results': serializer.data
        })
    
    elif request.method == 'POST':
        serializer = ApplicationCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            application = serializer.save()
            response_serializer = ApplicationDetailSerializer(application)
            
            return Response({
                'message': 'Application submitted successfully',
                'application': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def application_detail(request, pk):
    """
    Get detailed information about a specific application
    """
    if not hasattr(request.user, 'student'):
        return Response(
            {'error': 'Only students can access applications'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    application = get_object_or_404(
        Application,
        pk=pk,
        student=request.user.student
    )
    
    serializer = ApplicationDetailSerializer(application)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def application_pending(request):
    """
    Get all pending applications for the current student
    """
    if not hasattr(request.user, 'student'):
        return Response(
            {'error': 'Only students can access applications'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    applications = Application.objects.filter(
        student=request.user.student,
        status='pending'
    ).order_by('-applied_at')
    
    serializer = ApplicationListSerializer(applications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def application_accepted(request):
    """
    Get all accepted applications for the current student
    """
    if not hasattr(request.user, 'student'):
        return Response(
            {'error': 'Only students can access applications'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    applications = Application.objects.filter(
        student=request.user.student,
        status='accepted'
    ).order_by('-updated_at')
    
    serializer = ApplicationListSerializer(applications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def application_statistics(request):
    """
    Get application statistics for the current student
    """
    if not hasattr(request.user, 'student'):
        return Response(
            {'error': 'Only students can access applications'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    applications = Application.objects.filter(student=request.user.student)
    
    stats = {
        'total': applications.count(),
        'pending': applications.filter(status='pending').count(),
        'under_review': applications.filter(status='under_review').count(),
        'accepted': applications.filter(status='accepted').count(),
        'rejected': applications.filter(status='rejected').count(),
        'withdrawn': applications.filter(status='withdrawn').count(),
    }
    
    return Response(stats)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def application_withdraw(request, pk):
    """
    Withdraw an application
    """
    if not hasattr(request.user, 'student'):
        return Response(
            {'error': 'Only students can access applications'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    application = get_object_or_404(
        Application,
        pk=pk,
        student=request.user.student
    )
    
    # Check if application can be withdrawn
    if application.status in ['accepted', 'rejected']:
        return Response(
            {'error': 'Cannot withdraw an application that has been processed'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    application.status = 'withdrawn'
    application.save()
    
    serializer = ApplicationDetailSerializer(application)
    return Response({
        'message': 'Application withdrawn successfully',
        'application': serializer.data
    })