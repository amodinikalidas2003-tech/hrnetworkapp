package com.hrnetwork.app.form.service;

import com.hrnetwork.app.common.exception.ResourceNotFoundException;
import com.hrnetwork.app.form.dto.FormSchemaDTO;
import com.hrnetwork.app.form.entity.FormSchema;
import com.hrnetwork.app.form.mapper.FormSchemaMapper;
import com.hrnetwork.app.form.repository.FormSchemaRepository;
import com.hrnetwork.app.iam.entity.User;
import com.hrnetwork.app.iam.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

@Service
@RequiredArgsConstructor
public class FormSchemaService {

    private final FormSchemaRepository formSchemaRepository;
    private final FormSchemaMapper formSchemaMapper;
    private final UserRepository userRepository;

    @Transactional
    public FormSchemaDTO createFormSchema(FormSchemaDTO dto) {
        FormSchema entity = formSchemaMapper.toEntity(dto);
        
        // Fetch the user who created the form (in a real app, get from SecurityContext)
        User creator = userRepository.findById(dto.getCreatedById())
                .orElseThrow(() -> new ResourceNotFoundException("user.not.found"));
        
        entity.setCreatedBy(creator);
        
        FormSchema saved = formSchemaRepository.save(entity);
        return formSchemaMapper.toDto(saved);
    }

    @Transactional(readOnly = true)
    public Page<FormSchemaDTO> getAllFormSchemas(Pageable pageable) {
        return formSchemaRepository.findAll(pageable).map(formSchemaMapper::toDto);
    }

    @Transactional(readOnly = true)
    public FormSchemaDTO getFormSchemaById(UUID id) {
        FormSchema entity = formSchemaRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("error.not.found"));
        return formSchemaMapper.toDto(entity);
    }
}
