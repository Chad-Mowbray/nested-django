from django.shortcuts import render, redirect
from .models import Cohort, Student
from .forms import CohortForm, StudentForm

def get_cohort(cohort_id):
    return Cohort.objects.get(id=cohort_id)

def cohort_list(request):
    cohorts = Cohort.objects.all()
    return render(request, 'cohorts_and_students/cohorts_list.html', {'cohorts': cohorts})

def cohort_detail(request, cohort_id):
    cohort = get_cohort(cohort_id)
    return render(request, 'cohorts_and_students/cohort_detail.html', {'cohort': cohort})

def new_cohort(request):
    if request.method == "POST":
        form = CohortForm(request.POST)
        if form.is_valid():
            cohort = form.save(commit=False)
            cohort.save()
            return redirect('cohort_detail', cohort_id=cohort.id)
    else:
        form = CohortForm()
    return render(request, 'cohorts_and_students/cohort_form.html', {'form': form, 'type_of_request': 'New'})

def edit_cohort(request, cohort_id):
    cohort = get_cohort(cohort_id)
    if request.method == "POST":
        form = CohortForm(request.POST, instance=cohort)
        if form.is_valid():
            cohort = form.save(commit=False)
            cohort.save()
            return redirect('cohort_detail', cohort_id=cohort.id)
    else:
        form = CohortForm(instance=cohort)
    return render(request, 'cohorts_and_students/cohort_form.html', {'form': form, 'type_of_request': 'Edit'})

def delete_cohort(request, cohort_id):
    if request.method == "POST":
        cohort = get_cohort(cohort_id)
        cohort.delete()
    return redirect('cohort_list')

def get_student(student_id):
    return Student.objects.get(id=student_id)

def student_list(request, cohort_id):
    cohort = get_cohort(cohort_id)
    students = cohort.students.all()
    return render(request, 'cohorts_and_students/students_list.html', {'cohort': cohort, 'students': students})

def student_detail(request, cohort_id, student_id):
    cohort = get_cohort(cohort_id)
    student = Student.objects.get(slug=student_id)
    return render(request, 'cohorts_and_students/student_detail.html', {'cohort': cohort, 'student': student})

def new_student(request, cohort_id):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            cohort_id = request.get_full_path().split("/")[2]
            student.cohort = get_cohort(cohort_id)
            student.save()
            return redirect('student_detail', cohort_id=student.cohort.id, student_id=student.id)
    else:
        form = StudentForm()
    return render(request, 'cohorts_and_students/student_form.html', {'form': form, 'type_of_request': 'New'})

def edit_student(request, cohort_id, student_id):
    cohort = get_cohort(cohort_id)
    student = get_student(student_id)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            return redirect('student_detail', student_id=student.id, cohort_id=cohort_id)
    else:
        form = StudentForm(instance=student)
    return render(request, 'cohorts_and_students/student_form.html', {'form': form, 'type_of_request': 'Edit'})

def delete_student(request, cohort_id, student_id):
    if request.method == "POST":
        student = get_student(student_id)
        student.delete()
    return redirect('student_list', cohort_id=cohort_id)