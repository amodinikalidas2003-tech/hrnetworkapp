package com.hrnetwork.app.assessment.controller;

import com.hrnetwork.app.assessment.dto.AssessmentScoreDTO;
import com.hrnetwork.app.assessment.service.AssessmentScoreService;
import com.hrnetwork.app.common.dto.ApiResponse;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/assessments")
@RequiredArgsConstructor
public class AssessmentScoreController {

    private final AssessmentScoreService scoreService;

    @PostMapping
    public ResponseEntity<ApiResponse<AssessmentScoreDTO>> createScore(@Valid @RequestBody AssessmentScoreDTO dto) {
        AssessmentScoreDTO created = scoreService.createScore(dto);
        return ResponseEntity.ok(ApiResponse.success(created));
    }

    @GetMapping("/users/{userId}")
    public ResponseEntity<ApiResponse<List<AssessmentScoreDTO>>> getScoresForUser(@PathVariable UUID userId) {
        List<AssessmentScoreDTO> scores = scoreService.getScoresForUser(userId);
        return ResponseEntity.ok(ApiResponse.success(scores));
    }
}
