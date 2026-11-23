//! Minimal workspace core library with layered modular domains.
//!
//! # Examples
//!
//! ```
//! use skills_core::modules::math::MathModule;
//! use skills_core::modules::math::dto::MathError;
//!
//! let mut module = MathModule::new();
//! let res = module.controller.handle_add(15, 27)?;
//! assert_eq!(res.sum, 42);
//! # Ok::<(), MathError>(())
//! ```

pub mod modules;

/// Returns the crate identifier for smoke verification.
///
/// # Examples
///
/// ```
/// assert_eq!(skills_core::crate_name(), "skills-core");
/// ```
#[must_use]
pub const fn crate_name() -> &'static str {
    "skills-core"
}

#[cfg(test)]
mod tests {
    use super::crate_name;
    use super::modules::math::MathModule;

    #[test]
    fn returns_expected_name() {
        assert_eq!(crate_name(), "skills-core");
    }

    #[test]
    fn math_module_adds_and_tracks_history() {
        let mut module = MathModule::new();
        let res = module.controller.handle_add(15, 27).expect("valid addition");
        assert_eq!(res.sum, 42);
        assert_eq!(res.history_count, 1);
    }
}
