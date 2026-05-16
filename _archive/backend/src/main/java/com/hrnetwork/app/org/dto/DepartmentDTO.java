package com.hrnetwork.app.org.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;
import java.util.UUID;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class DepartmentDTO {
    private UUID id;

    @NotBlank
    private String name;

    private UUID parentId;
    
    private Instant createdAt;
    private Instant updatedAt;
}
