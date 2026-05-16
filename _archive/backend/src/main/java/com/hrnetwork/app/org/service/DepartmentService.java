package com.hrnetwork.app.org.service;

import com.hrnetwork.app.common.exception.ResourceNotFoundException;
import com.hrnetwork.app.org.dto.DepartmentDTO;
import com.hrnetwork.app.org.entity.Department;
import com.hrnetwork.app.org.mapper.DepartmentMapper;
import com.hrnetwork.app.org.repository.DepartmentRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

@Service
@RequiredArgsConstructor
public class DepartmentService {

    private final DepartmentRepository departmentRepository;
    private final DepartmentMapper departmentMapper;

    @Transactional
    public DepartmentDTO createDepartment(DepartmentDTO dto) {
        Department entity = departmentMapper.toEntity(dto);
        
        if (dto.getParentId() != null) {
            Department parent = departmentRepository.findById(dto.getParentId())
                    .orElseThrow(() -> new ResourceNotFoundException("Parent department not found"));
            entity.setParent(parent);
        }
        
        Department saved = departmentRepository.save(entity);
        return departmentMapper.toDto(saved);
    }

    @Transactional(readOnly = true)
    public Page<DepartmentDTO> getAllDepartments(Pageable pageable) {
        return departmentRepository.findAll(pageable).map(departmentMapper::toDto);
    }

    @Transactional(readOnly = true)
    public DepartmentDTO getDepartmentById(UUID id) {
        Department entity = departmentRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Department not found"));
        return departmentMapper.toDto(entity);
    }
}
