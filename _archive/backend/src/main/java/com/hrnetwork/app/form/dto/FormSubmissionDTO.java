package com.hrnetwork.app.form.dto;

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
public class FormSubmissionDTO {
    private UUID id;

    @NotNull
    private UUID schemaId;

    @NotNull
    private Map<String, Object> data;

    private UUID submittedById;
    private Instant createdAt;
    private Instant updatedAt;
}
