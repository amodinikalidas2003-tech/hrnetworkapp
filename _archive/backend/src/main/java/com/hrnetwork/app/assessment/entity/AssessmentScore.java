package com.hrnetwork.app.assessment.entity;

import com.hrnetwork.app.form.entity.FormSubmission;
import com.hrnetwork.app.iam.entity.User;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.UpdateTimestamp;
import org.hibernate.type.SqlTypes;

import java.time.Instant;
import java.util.Map;
import java.util.UUID;

@Entity
@Table(name = "assessment_scores")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AssessmentScore {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "evaluated_user_id", nullable = false)
    private User evaluatedUser;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "evaluator_user_id", nullable = false)
    private User evaluatorUser;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "form_submission_id")
    private FormSubmission submission;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(nullable = false)
    private Map<String, Double> dimensionScores; // Stores scores for different personality/work dimensions

    @Column(nullable = false)
    private Double totalScore;

    @CreationTimestamp
    @Column(updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    private Instant updatedAt;
}
