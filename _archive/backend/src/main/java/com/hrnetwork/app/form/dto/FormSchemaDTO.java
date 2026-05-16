package com.hrnetwork.app.form.dto;

import jakarta.validation.constraints.NotBlank;
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
public class FormSchemaDTO {
    private UUID id;

    @NotBlank(message = "{form.name.required}")
    private String name;

    private String description;

    @NotNull(message = "{form.schema.required}")
    private Map<String, Object> schemaDefinition;

    private UUID createdById;
    private Instant createdAt;
    private Instant updatedAt;
}
