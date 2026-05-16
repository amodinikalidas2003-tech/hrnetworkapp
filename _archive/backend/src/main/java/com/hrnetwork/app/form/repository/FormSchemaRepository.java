package com.hrnetwork.app.form.repository;

import com.hrnetwork.app.form.entity.FormSchema;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface FormSchemaRepository extends JpaRepository<FormSchema, UUID> {
}
