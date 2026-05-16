package com.hrnetwork.app.assessment.mapper;

import com.hrnetwork.app.assessment.dto.AssessmentScoreDTO;
import com.hrnetwork.app.assessment.entity.AssessmentScore;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public interface AssessmentScoreMapper {

    @Mapping(source = "evaluatedUser.id", target = "evaluatedUserId")
    @Mapping(source = "evaluatorUser.id", target = "evaluatorUserId")
    @Mapping(source = "submission.id", target = "submissionId")
    AssessmentScoreDTO toDto(AssessmentScore entity);

    @Mapping(target = "evaluatedUser", ignore = true)
    @Mapping(target = "evaluatorUser", ignore = true)
    @Mapping(target = "submission", ignore = true)
    AssessmentScore toEntity(AssessmentScoreDTO dto);
}
