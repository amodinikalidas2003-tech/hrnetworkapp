package com.hrnetwork.app.assessment.repository;

import com.hrnetwork.app.assessment.entity.AssessmentScore;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface AssessmentScoreRepository extends JpaRepository<AssessmentScore, UUID> {
    List<AssessmentScore> findByEvaluatedUserId(UUID evaluatedUserId);
    List<AssessmentScore> findByEvaluatorUserId(UUID evaluatorUserId);
}
