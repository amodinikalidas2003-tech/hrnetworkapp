package com.hrnetwork.app.dashboard.service;

import com.hrnetwork.app.assessment.repository.AssessmentScoreRepository;
import com.hrnetwork.app.dashboard.dto.HrDashboardStatsDTO;
import com.hrnetwork.app.form.entity.FormSchema;
import com.hrnetwork.app.form.repository.FormSchemaRepository;
import com.hrnetwork.app.form.repository.FormSubmissionRepository;
import com.hrnetwork.app.iam.repository.UserRepository;
import com.hrnetwork.app.org.repository.DepartmentRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashMap;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class DashboardService {

    private final UserRepository userRepository;
    private final DepartmentRepository departmentRepository;
    private final FormSchemaRepository formSchemaRepository;
    private final FormSubmissionRepository formSubmissionRepository;
    private final AssessmentScoreRepository assessmentScoreRepository;

    @Transactional(readOnly = true)
    public HrDashboardStatsDTO getGlobalStats() {
        long totalUsers = userRepository.count();
        long totalDepts = departmentRepository.count();
        long totalSchemas = formSchemaRepository.count();
        long totalSubmissions = formSubmissionRepository.count();

        // Very basic aggregation for demo purposes
        // In a real app with large data, this would be done with custom native queries or views
        Map<String, Long> submissionsByForm = new HashMap<>();
        for (FormSchema schema : formSchemaRepository.findAll()) {
            // This is just a placeholder, ideally use a GROUP BY query
            submissionsByForm.put(schema.getName(), 0L); 
        }

        double avgScore = 0.0;
        var scores = assessmentScoreRepository.findAll();
        if (!scores.isEmpty()) {
            avgScore = scores.stream()
                    .mapToDouble(s -> s.getTotalScore() != null ? s.getTotalScore() : 0.0)
                    .average()
                    .orElse(0.0);
        }

        return HrDashboardStatsDTO.builder()
                .totalUsers(totalUsers)
                .totalDepartments(totalDepts)
                .totalFormsCreated(totalSchemas)
                .totalFormSubmissions(totalSubmissions)
                .submissionsByForm(submissionsByForm)
                .averageOverallScore(avgScore)
                .build();
    }
}
