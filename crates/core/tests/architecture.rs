//! Architecture boundary tests verifying crate isolation.

use std::error::Error;
use std::fmt::{Debug, Display};
use std::fs;
use std::hash::Hash;
use std::path::Path;
use skills_core::modules::math::MathModule;
use skills_core::modules::math::controller::MathController;
use skills_core::modules::math::dto::{AddRequest, AddResponse, MathError};
use skills_core::modules::math::entity::CalculationEntry;
use skills_core::modules::math::repository::{InMemoryMathRepository, MathRepository};
use skills_core::modules::math::service::MathService;

const fn assert_send_sync_debug<T: Send + Sync + Debug + 'static>() {}
const fn assert_value_type<T: Send + Sync + Debug + Clone + Copy + PartialEq + Eq + Hash + 'static>()
{
}
const fn assert_repo_type<T: Send + Sync + Debug + Clone + PartialEq + Eq + Default + 'static>() {}
const fn assert_error_type<
    T: Error + Display + Send + Sync + Debug + Clone + Copy + PartialEq + Eq + Hash + 'static,
>() {
}
const fn assert_default<T: Default>() {}

const _: () = {
    assert_value_type::<CalculationEntry>();
    assert_value_type::<AddRequest>();
    assert_value_type::<AddResponse>();
    assert_error_type::<MathError>();
    assert_repo_type::<InMemoryMathRepository>();
    assert_send_sync_debug::<Box<dyn MathRepository>>();
    assert_send_sync_debug::<MathService>();
    assert_send_sync_debug::<MathController>();
    assert_send_sync_debug::<MathModule>();
    assert_default::<MathModule>();
};

#[test]
fn public_error_enforces_non_exhaustive_and_good_err_contracts() {
    let errors = [
        MathError::OperandOutOfBounds {
            limit: 1_000_000_000,
        },
        MathError::Overflow,
    ];
    for err in errors {
        // Requires #[non_exhaustive]; removing it trips `unreachable_patterns` under `-D warnings`.
        let label = match err {
            MathError::OperandOutOfBounds { .. } => "bounds",
            MathError::Overflow => "overflow",
            _ => "unknown",
        };
        assert_ne!(label, "unknown", "known MathError variant must match");

        let display = err.to_string();
        assert_ne!(display, "", "Display output must not be empty");
        assert!(
            !display.ends_with('.'),
            "Display message must not end with punctuation: {display}"
        );
        assert!(
            display.chars().next().is_some_and(char::is_lowercase),
            "Display message must start lowercase: {display}"
        );
        assert_ne!(
            format!("{err:?}"),
            "",
            "Debug output must not be empty"
        );
    }
}

#[test]
fn core_never_depends_on_xtask() {
    let manifest = Path::new(env!("CARGO_MANIFEST_DIR")).join("Cargo.toml");
    let content = fs::read_to_string(manifest).expect("read core Cargo.toml");
    assert!(
        !content.contains("xtask"),
        "core crate must never depend on xtask"
    );
}

#[test]
fn workspace_enforces_forbid_unsafe_code() {
    let root_manifest = Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .and_then(|p| p.parent())
        .expect("workspace root")
        .join("Cargo.toml");
    let content = fs::read_to_string(root_manifest).expect("read workspace Cargo.toml");
    assert!(
        content.contains("unsafe_code = \"forbid\""),
        "workspace must forbid unsafe_code"
    );
}

#[test]
fn workspace_locks_immutable_lint_policy() {
    let root_manifest = Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .and_then(|p| p.parent())
        .expect("workspace root")
        .join("Cargo.toml");
    let content = fs::read_to_string(root_manifest).expect("read workspace Cargo.toml");

    assert!(
        !content.contains("unsafe_code = \"warn\"") && !content.contains("unsafe_code = \"allow\""),
        "unsafe_code must never be weakened to warn or allow"
    );

    let required_entries = [
        "rust-version = \"1.85\"",
        "unsafe_code = \"forbid\"",
        "missing_debug_implementations = \"warn\"",
        "missing_docs = \"warn\"",
        "unreachable_pub = \"warn\"",
        "rust_2018_idioms = { level = \"warn\", priority = -1 }",
        "all = { level = \"warn\", priority = -1 }",
        "pedantic = { level = \"warn\", priority = -1 }",
        "unwrap_used = \"warn\"",
        "expect_used = \"allow\"",
        "panic_in_result_fn = \"warn\"",
        "missing_panics_doc = \"warn\"",
        "missing_errors_doc = \"warn\"",
        "missing_assert_message = \"warn\"",
        "allow_attributes = \"warn\"",
        "allow_attributes_without_reason = \"warn\"",
        "undocumented_unsafe_blocks = \"warn\"",
        "multiple_unsafe_ops_per_block = \"warn\"",
        "fn_params_excessive_bools = \"warn\"",
        "struct_excessive_bools = \"warn\"",
        "clone_on_ref_ptr = \"warn\"",
        "redundant_clone = \"warn\"",
        "rc_buffer = \"warn\"",
        "exhaustive_enums = \"warn\"",
        "string_add = \"warn\"",
        "wildcard_imports = \"warn\"",
        "dbg_macro = \"warn\"",
        "todo = \"warn\"",
        "print_stdout = \"warn\"",
        "print_stderr = \"warn\"",
        "as_conversions = \"warn\"",
        "cast_possible_truncation = \"warn\"",
        "cast_sign_loss = \"warn\"",
        "missing_copy_implementations = \"warn\"",
        "trivial_casts = \"warn\"",
        "trivial_numeric_casts = \"warn\"",
        "meta_variable_misuse = \"warn\"",
        "unused_lifetimes = \"warn\"",
        "unused_import_braces = \"warn\"",
        "non_ascii_idents = \"warn\"",
        "[workspace.lints.rustdoc]",
        "broken_intra_doc_links = \"warn\"",
        "private_intra_doc_links = \"warn\"",
        "missing_crate_level_docs = \"warn\"",
        "private_doc_tests = \"warn\"",
        "invalid_codeblock_attributes = \"warn\"",
        "invalid_rust_codeblocks = \"warn\"",
        "invalid_html_tags = \"warn\"",
        "bare_urls = \"warn\"",
        "redundant_explicit_links = \"warn\"",
        "unescaped_backticks = \"warn\"",
        "unimplemented = \"warn\"",
        "map_err_ignore = \"warn\"",
        "get_unwrap = \"warn\"",
        "unwrap_in_result = \"warn\"",
        "fallible_impl_from = \"warn\"",
        "derive_partial_eq_without_eq = \"warn\"",
        "same_name_method = \"warn\"",
        "partial_pub_fields = \"warn\"",
        "rest_pat_in_fully_bound_structs = \"warn\"",
        "empty_structs_with_brackets = \"warn\"",
        "empty_enum_variants_with_brackets = \"warn\"",
        "rc_mutex = \"warn\"",
        "mutex_atomic = \"warn\"",
        "mutex_integer = \"warn\"",
        "mem_forget = \"warn\"",
        "lossy_float_literal = \"warn\"",
        "negative_feature_names = \"warn\"",
        "redundant_feature_names = \"warn\"",
        "wildcard_dependencies = \"warn\"",
    ];

    for entry in required_entries {
        assert!(
            content.contains(entry),
            "workspace Cargo.toml missing required lint policy entry: {entry}"
        );
    }
}

#[test]
fn workspace_locks_clippy_toml() {
    let clippy_toml = Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .and_then(|p| p.parent())
        .expect("workspace root")
        .join("clippy.toml");
    let content = fs::read_to_string(clippy_toml).expect("read workspace clippy.toml");

    let required_entries = [
        "max-fn-params-bools = 0",
        "allow-unwrap-in-tests = true",
        "allow-expect-in-tests = true",
        "allow-print-in-tests = true",
    ];

    for entry in required_entries {
        assert!(
            content.contains(entry),
            "clippy.toml missing required policy setting: {entry}"
        );
    }
}

#[test]
fn xtask_locks_doc_and_doctest_gates() {
    let main_rs = Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .and_then(|p| p.parent())
        .expect("workspace root")
        .join("crates/xtask/src/main.rs");
    let content = fs::read_to_string(main_rs).expect("read xtask main.rs");
    for token in [
        "\"-D warnings\"",
        "RUSTDOCFLAGS",
        "\"--doc\"",
        "\"--all-features\"",
        "\"--no-deps\"",
    ] {
        assert!(
            content.contains(token),
            "xtask validate must keep gate token: {token}"
        );
    }
    assert!(
        !content.contains("cargo fmt") && !content.contains("\"fmt\""),
        "formatters must never run in xtask validate"
    );
}
