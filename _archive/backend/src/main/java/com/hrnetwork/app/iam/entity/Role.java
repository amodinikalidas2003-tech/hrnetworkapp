package com.hrnetwork.app.iam.entity;

public enum Role {
    SUPER_ADMIN,
    ADMIN, // Can create forms
    MANAGER, // Can view department data
    USER // Can submit forms
}
