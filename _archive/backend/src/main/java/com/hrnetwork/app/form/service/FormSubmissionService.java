package com.hrnetwork.app.form.service;

import com.hrnetwork.app.common.exception.ResourceNotFoundException;
import com.hrnetwork.app.form.dto.FormSubmissionDTO;
import com.hrnetwork.app.form.entity.FormSchema;
import com.hrnetwork.app.form.entity.FormSubmission;
import com.hrnetwork.app.form.mapper.FormSubmissionMapper;
import com.hrnetwork.app.form.repository.FormSchemaRepository;
import com.hrnetwork.app.form.repository.FormSubmissionRepository;
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
public class FormSubmissionService {

    private final FormSubmissionRepository formSubmissionRepository;
    private final FormSubmissionMapper formSubmissionMapper;
    private final FormSchemaRepository formSchemaRepository;
    private final UserRepository userRepository;

    @Transactional
    public FormSubmissionDTO submitForm(FormSubmissionDTO dto) {
        FormSchema schema = formSchemaRepository.findById(dto.getSchemaId())
                .orElseThrow(() -> new ResourceNotFoundException("error.not.found"));

        User submitter = userRepository.findById(dto.getSubmittedById())
                .orElseThrow(() -> new ResourceNotFoundException("user.not.found"));

        FormSubmission entity = formSubmissionMapper.toEntity(dto);
        entity.setSchema(schema);
        entity.setSubmittedBy(submitter);

        FormSubmission saved = formSubmissionRepository.save(entity);
        return formSubmissionMapper.toDto(saved);
    }

    @Transactional(readOnly = true)
    public Page<FormSubmissionDTO> getAllSubmissions(Pageable pageable) {
        return formSubmissionRepository.findAll(pageable).map(formSubmissionMapper::toDto);
    }
}
