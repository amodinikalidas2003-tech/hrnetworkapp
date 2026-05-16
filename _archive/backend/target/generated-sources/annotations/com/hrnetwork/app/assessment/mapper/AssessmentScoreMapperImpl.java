package com.hrnetwork.app.assessment.mapper;

import com.hrnetwork.app.assessment.dto.AssessmentScoreDTO;
import com.hrnetwork.app.assessment.entity.AssessmentScore;
import com.hrnetwork.app.form.entity.FormSubmission;
import com.hrnetwork.app.iam.entity.User;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.UUID;
import javax.annotation.processing.Generated;
import org.springframework.stereotype.Component;

@Generated(
    value = "org.mapstruct.ap.MappingProcessor",
    date = "2026-03-13T22:25:24+0330",
    comments = "version: 1.5.5.Final, compiler: javac, environment: Java 21.0.10 (Microsoft)"
)
@Component
public class AssessmentScoreMapperImpl implements AssessmentScoreMapper {

    @Override
    public AssessmentScoreDTO toDto(AssessmentScore entity) {
        if ( entity == null ) {
            return null;
        }

        AssessmentScoreDTO.AssessmentScoreDTOBuilder assessmentScoreDTO = AssessmentScoreDTO.builder();

        assessmentScoreDTO.evaluatedUserId( entityEvaluatedUserId( entity ) );
        assessmentScoreDTO.evaluatorUserId( entityEvaluatorUserId( entity ) );
        assessmentScoreDTO.submissionId( entitySubmissionId( entity ) );
        assessmentScoreDTO.id( entity.getId() );
        Map<String, Double> map = entity.getDimensionScores();
        if ( map != null ) {
            assessmentScoreDTO.dimensionScores( new LinkedHashMap<String, Double>( map ) );
        }
        assessmentScoreDTO.totalScore( entity.getTotalScore() );
        assessmentScoreDTO.createdAt( entity.getCreatedAt() );
        assessmentScoreDTO.updatedAt( entity.getUpdatedAt() );

        return assessmentScoreDTO.build();
    }

    @Override
    public AssessmentScore toEntity(AssessmentScoreDTO dto) {
        if ( dto == null ) {
            return null;
        }

        AssessmentScore.AssessmentScoreBuilder assessmentScore = AssessmentScore.builder();

        assessmentScore.id( dto.getId() );
        Map<String, Double> map = dto.getDimensionScores();
        if ( map != null ) {
            assessmentScore.dimensionScores( new LinkedHashMap<String, Double>( map ) );
        }
        assessmentScore.totalScore( dto.getTotalScore() );
        assessmentScore.createdAt( dto.getCreatedAt() );
        assessmentScore.updatedAt( dto.getUpdatedAt() );

        return assessmentScore.build();
    }

    private UUID entityEvaluatedUserId(AssessmentScore assessmentScore) {
        if ( assessmentScore == null ) {
            return null;
        }
        User evaluatedUser = assessmentScore.getEvaluatedUser();
        if ( evaluatedUser == null ) {
            return null;
        }
        UUID id = evaluatedUser.getId();
        if ( id == null ) {
            return null;
        }
        return id;
    }

    private UUID entityEvaluatorUserId(AssessmentScore assessmentScore) {
        if ( assessmentScore == null ) {
            return null;
        }
        User evaluatorUser = assessmentScore.getEvaluatorUser();
        if ( evaluatorUser == null ) {
            return null;
        }
        UUID id = evaluatorUser.getId();
        if ( id == null ) {
            return null;
        }
        return id;
    }

    private UUID entitySubmissionId(AssessmentScore assessmentScore) {
        if ( assessmentScore == null ) {
            return null;
        }
        FormSubmission submission = assessmentScore.getSubmission();
        if ( submission == null ) {
            return null;
        }
        UUID id = submission.getId();
        if ( id == null ) {
            return null;
        }
        return id;
    }
}
