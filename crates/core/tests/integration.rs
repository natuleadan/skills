//! Integration tests verifying public API contracts and module boundaries.

use std::fs;
use std::path::Path;
use skills_core::crate_name;
use skills_core::modules::math::MathModule;
use skills_core::modules::math::dto::MathError;

#[test]
fn public_api_contract_is_stable() {
    assert_eq!(crate_name(), "skills-core");
}

#[test]
fn math_module_integration_and_validation() {
    let mut module = MathModule::new();
    let first = module.controller.handle_add(10, 32).expect("valid sum");
    assert_eq!(first.sum, 42);
    assert_eq!(first.history_count, 1);

    let err = module
        .controller
        .handle_add(2_000_000_000, 1)
        .expect_err("out-of-bounds operand must fail");
    assert!(matches!(err, MathError::OperandOutOfBounds { .. }));
    assert_ne!(err.to_string(), "");
}

#[test]
fn enforces_modular_layer_boundaries() {
    let math_dir = Path::new(env!("CARGO_MANIFEST_DIR")).join("src/modules/math");
    let entity = fs::read_to_string(math_dir.join("entity.rs")).expect("read entity.rs");
    let dto = fs::read_to_string(math_dir.join("dto.rs")).expect("read dto.rs");
    let repo = fs::read_to_string(math_dir.join("repository.rs")).expect("read repository.rs");
    let service = fs::read_to_string(math_dir.join("service.rs")).expect("read service.rs");
    let controller =
        fs::read_to_string(math_dir.join("controller.rs")).expect("read controller.rs");

    for forbidden in ["service", "controller", "repository"] {
        assert!(!entity.contains(forbidden), "entity.rs leaked {forbidden}");
        assert!(!dto.contains(forbidden), "dto.rs leaked {forbidden}");
    }
    assert!(!repo.contains("service") && !repo.contains("controller"));
    assert!(!service.contains("controller"));
    assert!(!controller.contains("repository"));
}
