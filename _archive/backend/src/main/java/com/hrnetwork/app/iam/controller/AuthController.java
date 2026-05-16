package com.hrnetwork.app.iam.controller;

import com.hrnetwork.app.common.dto.ApiResponse;
import com.hrnetwork.app.iam.dto.LoginRequest;
import com.hrnetwork.app.iam.dto.LoginResponse;
import com.hrnetwork.app.iam.dto.UserDTO;
import com.hrnetwork.app.iam.entity.User;
import com.hrnetwork.app.iam.mapper.UserMapper;
import com.hrnetwork.app.iam.repository.UserRepository;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/auth")
@RequiredArgsConstructor
public class AuthController {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final UserMapper userMapper;

    @PostMapping("/login")
    public ResponseEntity<ApiResponse<LoginResponse>> login(@Valid @RequestBody LoginRequest request) {
        User user = userRepository.findByEmail(request.getEmail())
                .orElse(null);

        if (user == null || !passwordEncoder.matches(request.getPassword(), user.getPassword())) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(ApiResponse.error("Invalid email or password"));
        }

        // Mock Token for now (In a real app, generate a JWT string here)
        String mockToken = "jwt_token_placeholder_for_" + user.getId();

        UserDTO userDto = userMapper.toDto(user);
        LoginResponse response = new LoginResponse(mockToken, userDto);

        return ResponseEntity.ok(ApiResponse.success(response));
    }
}
