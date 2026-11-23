//! Persistence port and in-memory adapter for math calculations.

use super::entity::CalculationEntry;

/// Storage abstraction for [`CalculationEntry`] records.
pub trait MathRepository: std::fmt::Debug + Send + Sync {
    /// Persists a completed calculation entry.
    fn save(&mut self, entry: CalculationEntry);
    /// Returns the total number of stored entries.
    fn count(&self) -> usize;
    /// Returns all stored calculation entries in insertion order.
    fn list(&self) -> &[CalculationEntry];
}

/// In-memory calculation store implementing [`MathRepository`].
///
/// # Examples
///
/// ```
/// use skills_core::modules::math::entity::CalculationEntry;
/// use skills_core::modules::math::repository::{InMemoryMathRepository, MathRepository};
///
/// let mut store = InMemoryMathRepository::new();
/// store.save(CalculationEntry { a: 1, b: 2, sum: 3 });
/// assert_eq!(store.count(), 1);
/// ```
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct InMemoryMathRepository {
    entries: Vec<CalculationEntry>,
}

impl InMemoryMathRepository {
    /// Creates an empty in-memory calculation repository.
    #[must_use]
    pub const fn new() -> Self {
        Self {
            entries: Vec::new(),
        }
    }
}

impl MathRepository for InMemoryMathRepository {
    fn save(&mut self, entry: CalculationEntry) {
        self.entries.push(entry);
    }

    fn count(&self) -> usize {
        self.entries.len()
    }

    fn list(&self) -> &[CalculationEntry] {
        &self.entries
    }
}
