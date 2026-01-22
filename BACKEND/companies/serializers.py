# companies/serializers.py
from rest_framework import serializers
from .models import Company, Internship

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'company_name', 'email', 'phone', 'address', 
                  'industry', 'description', 'website', 'logo', 
                  'is_approved', 'created_at']
        read_only_fields = ['id', 'created_at', 'is_approved']


class InternshipListSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.company_name', read_only=True)
    company_logo = serializers.ImageField(source='company.logo', read_only=True)
    
    class Meta:
        model = Internship
        fields = ['id', 'company', 'company_name', 'company_logo', 'title', 
                  'description', 'placement_type', 'duration_months', 
                  'positions_available', 'location', 'stipend', 
                  'application_deadline', 'start_date', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class InternshipDetailSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    applications_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Internship
        fields = ['id', 'company', 'title', 'description', 'requirements',
                  'placement_type', 'duration_months', 'positions_available', 
                  'location', 'stipend', 'application_deadline', 'start_date', 
                  'is_active', 'applications_count', 'created_at']
    
    def get_applications_count(self, obj):
        return obj.applications.count()


# applications/serializers.py
from rest_framework import serializers
from .models import Application
from companies.serializers import InternshipListSerializer

class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['internship', 'cover_letter']
    
    def validate(self, data):
        student = self.context['request'].user.student
        internship = data['internship']
        
        # Check if student already applied
        if Application.objects.filter(student=student, internship=internship).exists():
            raise serializers.ValidationError("You have already applied for this internship.")
        
        # Check if internship is still active
        if not internship.is_active:
            raise serializers.ValidationError("This internship is no longer accepting applications.")
        
        # Check application deadline
        from django.utils import timezone
        if internship.application_deadline < timezone.now().date():
            raise serializers.ValidationError("The application deadline has passed.")
        
        return data
    
    def create(self, validated_data):
        validated_data['student'] = self.context['request'].user.student
        return super().create(validated_data)


class ApplicationListSerializer(serializers.ModelSerializer):
    internship = InternshipListSerializer(read_only=True)
    student_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Application
        fields = ['id', 'student_name', 'internship', 'status', 
                  'admin_approved', 'applied_at', 'updated_at']
        read_only_fields = ['id', 'applied_at', 'updated_at']
    
    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"


class ApplicationDetailSerializer(serializers.ModelSerializer):
    internship = InternshipDetailSerializer(read_only=True)
    student_name = serializers.SerializerMethodField()
    student_email = serializers.EmailField(source='student.email', read_only=True)
    
    class Meta:
        model = Application
        fields = ['id', 'student_name', 'student_email', 'internship', 
                  'cover_letter', 'status', 'admin_approved', 
                  'company_feedback', 'admin_notes', 'applied_at', 'updated_at']
        read_only_fields = ['id', 'applied_at', 'updated_at', 'status', 
                           'admin_approved', 'company_feedback', 'admin_notes']
    
    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"