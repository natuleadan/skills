//! Data transfer objects and input validation for math operations.

use std::fmt;

const MAX_OPERAND_ABS: i64 = 1_000_000_000;

/// Domain errors returned by validated math operations.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
#[non_exhaustive]
pub enum MathError {
    /// One or both operands exceeded the allowed safe bounds.
    OperandOutOfBounds {
        /// Maximum permitted absolute operand value.
        limit: i64,
    },
    /// The addition overflowed `i64`.
    Overflow,
}

impl fmt::Display for MathError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::OperandOutOfBounds { limit } => {
                write!(f, "operand exceeds safe limit of {limit}")
            }
            Self::Overflow => f.write_str("integer overflow during addition"),
        }
    }
}

impl std::error::Error for MathError {}

/// Request payload for addition.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct AddRequest {
    /// Left addend.
    pub a: i64,
    /// Right addend.
    pub b: i64,
}

impl AddRequest {
    /// Validates operand bounds before domain execution.
    ///
    /// # Errors
    /// Returns [`MathError::OperandOutOfBounds`] when an operand exceeds allowed bounds.
    ///
    /// # Examples
    ///
    /// ```
    /// use skills_core::modules::math::dto::{AddRequest, MathError};
    ///
    /// AddRequest { a: 1, b: 2 }.validate()?;
    /// assert!(AddRequest { a: 2_000_000_000, b: 0 }.validate().is_err());
    /// # Ok::<(), MathError>(())
    /// ```
    pub const fn validate(self) -> Result<(), MathError> {
        if self.a.saturating_abs() > MAX_OPERAND_ABS || self.b.saturating_abs() > MAX_OPERAND_ABS {
            return Err(MathError::OperandOutOfBounds {
                limit: MAX_OPERAND_ABS,
            });
        }
        Ok(())
    }
}

/// Response payload returned after addition.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct AddResponse {
    /// Sum of `a` and `b`.
    pub sum: i64,
    /// Number of calculations recorded after this operation.
    pub history_count: usize,
}
