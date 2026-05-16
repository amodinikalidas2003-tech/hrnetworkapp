package com.hrnetwork.app.common.config;

import com.hrnetwork.app.iam.entity.Role;
import com.hrnetwork.app.iam.entity.User;
import com.hrnetwork.app.iam.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class DatabaseSeeder implements CommandLineRunner {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    @Override
    public void run(String... args) {
        // Seed default admin if it doesn't exist
        if (userRepository.findByEmail("admin@vuexy.com").isEmpty()) {
            User admin = User.builder()
                    .username("admin")
                    .email("admin@vuexy.com")
                    .password(passwordEncoder.encode("admin"))
                    .role(Role.SUPER_ADMIN)
                    .build();

            userRepository.save(admin);
            System.out.println("Default Admin User Seeded (admin@vuexy.com / admin)");
        }
    }
}
