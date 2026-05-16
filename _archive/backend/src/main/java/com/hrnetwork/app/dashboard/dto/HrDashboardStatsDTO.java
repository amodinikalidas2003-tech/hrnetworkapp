package com.hrnetwork.app.dashboard.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Map;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class HrDashboardStatsDTO {
    private long totalUsers;
    private long totalDepartments;
    private long totalFormsCreated;
    private long totalFormSubmissions;
    private Map<String, Long> submissionsByForm;
    private double averageOverallScore;
}
