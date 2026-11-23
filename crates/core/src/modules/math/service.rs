//! Business logic service for math operations.

use super::dto::{AddRequest, AddResponse, MathError};
use super::entity::CalculationEntry;
use super::repository::MathRepository;

/// Orchestrates validated addition and history persistence.
#[derive(Debug)]
pub struct MathService {
    repo: Box<dyn MathRepository>,
}

impl MathService {
    /// Constructs a service backed by a [`MathRepository`] implementation.
    #[must_use]
    pub fn new(repo: Box<dyn MathRepository>) -> Self {
        Self { repo }
    }

    /// Validates, sums, and records an [`AddRequest`], returning an [`AddResponse`].
    ///
    /// # Errors
    /// Returns [`MathError`] if validation fails or integer overflow occurs.
    ///
    /// # Examples
    ///
    /// ```
    /// use skills_core::modules::math::dto::{AddRequest, MathError};
    /// use skills_core::modules::math::repository::InMemoryMathRepository;
    /// use skills_core::modules::math::service::MathService;
    ///
    /// let mut svc = MathService::new(Box::new(InMemoryMathRepository::new()));
    /// let res = svc.add(AddRequest { a: 1, b: 2 })?;
    /// assert_eq!(res.sum, 3);
    /// # Ok::<(), MathError>(())
    /// ```
    pub fn add(&mut self, req: AddRequest) -> Result<AddResponse, MathError> {
        req.validate()?;
        let sum = req.a.checked_add(req.b).ok_or(MathError::Overflow)?;
        self.repo.save(CalculationEntry {
            a: req.a,
            b: req.b,
            sum,
        });
        Ok(AddResponse {
            sum,
            history_count: self.repo.count(),
        })
    }
}
