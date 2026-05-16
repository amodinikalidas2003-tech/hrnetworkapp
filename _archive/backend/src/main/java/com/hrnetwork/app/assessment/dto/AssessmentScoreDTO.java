package com.hrnetwork.app.assessment.dto;

import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;
import java.util.Map;
import java.util.UUID;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AssessmentScoreDTO {
    private UUID id;

    @NotNull
    private UUID evaluatedUserId;

    @NotNull
    private UUID evaluatorUserId;

    private UUID submissionId;

    @NotNull
    private Map<String, Double> dimensionScores;

    private Double totalScore;

    private Instant createdAt;
    private Instant updatedAt;
}
