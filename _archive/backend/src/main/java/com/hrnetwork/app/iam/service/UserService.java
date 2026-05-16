package com.hrnetwork.app.iam.service;

import com.hrnetwork.app.common.exception.ResourceNotFoundException;
import com.hrnetwork.app.iam.dto.UserDTO;
import com.hrnetwork.app.iam.entity.User;
import com.hrnetwork.app.iam.mapper.UserMapper;
import com.hrnetwork.app.iam.repository.UserRepository;
import com.hrnetwork.app.org.entity.Department;
import com.hrnetwork.app.org.repository.DepartmentRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final UserMapper userMapper;
    private final DepartmentRepository departmentRepository;

    @Transactional
    public UserDTO createUser(UserDTO dto) {
        User entity = userMapper.toEntity(dto);
        
        // Mock password hashing for now
        entity.setPassword("encoded_password");

        if (dto.getDepartmentId() != null) {
            Department dept = departmentRepository.findById(dto.getDepartmentId())
                    .orElseThrow(() -> new ResourceNotFoundException("Department not found"));
            entity.setDepartment(dept);
        }

        User saved = userRepository.save(entity);
        return userMapper.toDto(saved);
    }

    @Transactional(readOnly = true)
    public Page<UserDTO> getAllUsers(Pageable pageable) {
        return userRepository.findAll(pageable).map(userMapper::toDto);
    }

    @Transactional(readOnly = true)
    public UserDTO getUserById(UUID id) {
        User entity = userRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("user.not.found"));
        return userMapper.toDto(entity);
    }
}
