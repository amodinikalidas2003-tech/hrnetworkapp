package com.hrnetwork.app.assessment.service;

import com.hrnetwork.app.assessment.dto.AssessmentScoreDTO;
import com.hrnetwork.app.assessment.entity.AssessmentScore;
import com.hrnetwork.app.assessment.mapper.AssessmentScoreMapper;
import com.hrnetwork.app.assessment.repository.AssessmentScoreRepository;
import com.hrnetwork.app.common.exception.ResourceNotFoundException;
import com.hrnetwork.app.form.entity.FormSubmission;
import com.hrnetwork.app.form.repository.FormSubmissionRepository;
import com.hrnetwork.app.iam.entity.User;
import com.hrnetwork.app.iam.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class AssessmentScoreService {

    private final AssessmentScoreRepository scoreRepository;
    private final AssessmentScoreMapper scoreMapper;
    private final UserRepository userRepository;
    private final FormSubmissionRepository submissionRepository;

    @Transactional
    public AssessmentScoreDTO createScore(AssessmentScoreDTO dto) {
        AssessmentScore entity = scoreMapper.toEntity(dto);

        User evaluated = userRepository.findById(dto.getEvaluatedUserId())
                .orElseThrow(() -> new ResourceNotFoundException("Evaluated user not found"));
        
        User evaluator = userRepository.findById(dto.getEvaluatorUserId())
                .orElseThrow(() -> new ResourceNotFoundException("Evaluator user not found"));

        entity.setEvaluatedUser(evaluated);
        entity.setEvaluatorUser(evaluator);

        if (dto.getSubmissionId() != null) {
            FormSubmission submission = submissionRepository.findById(dto.getSubmissionId())
                    .orElseThrow(() -> new ResourceNotFoundException("Form submission not found"));
            entity.setSubmission(submission);
        }

        // Calculate total score based on dimension scores if not provided
        if (dto.getTotalScore() == null && dto.getDimensionScores() != null) {
            double total = dto.getDimensionScores().values().stream()
                    .mapToDouble(Double::doubleValue)
                    .sum();
            entity.setTotalScore(total);
        } else {
            entity.setTotalScore(dto.getTotalScore());
        }

        AssessmentScore saved = scoreRepository.save(entity);
        return scoreMapper.toDto(saved);
    }

    @Transactional(readOnly = true)
    public List<AssessmentScoreDTO> getScoresForUser(UUID userId) {
        return scoreRepository.findByEvaluatedUserId(userId).stream()
                .map(scoreMapper::toDto)
                .collect(Collectors.toList());
    }
}
