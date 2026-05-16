package com.hrnetwork.app.form.repository;

import com.hrnetwork.app.form.entity.FormSubmission;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface FormSubmissionRepository extends JpaRepository<FormSubmission, UUID> {
}
