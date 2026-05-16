package com.hrnetwork.app.file.dto;

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
public class FileArchiveDTO {
    private UUID id;
    private String originalFileName;
    private String contentType;
    private Long size;
    private UUID uploadedById;
    private Instant createdAt;
}
