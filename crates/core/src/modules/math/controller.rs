//! Transport-facing controller for the math domain.

use super::dto::{AddRequest, AddResponse, MathError};
use super::service::MathService;

/// Entrypoint adapter delegating validated requests to [`MathService`].
#[derive(Debug)]
pub struct MathController {
    service: MathService,
}

impl MathController {
    /// Constructs a controller from a configured [`MathService`].
    #[must_use]
    pub const fn new(service: MathService) -> Self {
        Self { service }
    }

    /// Handles an addition request and returns the [`AddResponse`].
    ///
    /// # Errors
    /// Propagates [`MathError`] from [`MathService`].
    ///
    /// # Examples
    ///
    /// ```
    /// use skills_core::modules::math::MathModule;
    /// use skills_core::modules::math::dto::MathError;
    ///
    /// let mut module = MathModule::new();
    /// let res = module.controller.handle_add(2, 3)?;
    /// assert_eq!(res.sum, 5);
    /// # Ok::<(), MathError>(())
    /// ```
    pub fn handle_add(&mut self, a: i64, b: i64) -> Result<AddResponse, MathError> {
        self.service.add(AddRequest { a, b })
    }
}
