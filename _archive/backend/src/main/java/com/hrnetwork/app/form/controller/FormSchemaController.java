package com.hrnetwork.app.form.controller;

import com.hrnetwork.app.common.dto.ApiResponse;
import com.hrnetwork.app.form.dto.FormSchemaDTO;
import com.hrnetwork.app.form.service.FormSchemaService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequestMapping("/api/v1/forms/schemas")
@RequiredArgsConstructor
public class FormSchemaController {

    private final FormSchemaService formSchemaService;

    @PostMapping
    public ResponseEntity<ApiResponse<FormSchemaDTO>> createSchema(@Valid @RequestBody FormSchemaDTO dto) {
        FormSchemaDTO created = formSchemaService.createFormSchema(dto);
        return ResponseEntity.ok(ApiResponse.success(created));
    }

    @GetMapping
    public ResponseEntity<ApiResponse<Page<FormSchemaDTO>>> getAllSchemas(Pageable pageable) {
        Page<FormSchemaDTO> schemas = formSchemaService.getAllFormSchemas(pageable);
        return ResponseEntity.ok(ApiResponse.success(schemas));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<FormSchemaDTO>> getSchemaById(@PathVariable UUID id) {
        FormSchemaDTO schema = formSchemaService.getFormSchemaById(id);
        return ResponseEntity.ok(ApiResponse.success(schema));
    }
}
