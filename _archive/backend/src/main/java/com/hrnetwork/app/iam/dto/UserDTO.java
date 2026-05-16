package com.hrnetwork.app.iam.dto;

import com.hrnetwork.app.iam.entity.Role;
import jakarta.validation.constraints.Email;
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
public class UserDTO {
    private UUID id;

    @NotBlank
    private String username;

    @NotBlank(message = "{user.email.required}")
    @Email(message = "{user.email.invalid}")
    private String email;

    private Role role;
    private UUID departmentId;
    
    private Instant createdAt;
    private Instant updatedAt;
}
