package com.hrnetwork.app.form.controller;

import com.hrnetwork.app.common.dto.ApiResponse;
import com.hrnetwork.app.form.dto.FormSubmissionDTO;
import com.hrnetwork.app.form.service.FormSubmissionService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/forms/submissions")
@RequiredArgsConstructor
public class FormSubmissionController {

    private final FormSubmissionService formSubmissionService;

    @PostMapping
    public ResponseEntity<ApiResponse<FormSubmissionDTO>> submitForm(@Valid @RequestBody FormSubmissionDTO dto) {
        FormSubmissionDTO created = formSubmissionService.submitForm(dto);
        return ResponseEntity.ok(ApiResponse.success(created));
    }

    @GetMapping
    public ResponseEntity<ApiResponse<Page<FormSubmissionDTO>>> getAllSubmissions(Pageable pageable) {
        Page<FormSubmissionDTO> submissions = formSubmissionService.getAllSubmissions(pageable);
        return ResponseEntity.ok(ApiResponse.success(submissions));
    }
}
