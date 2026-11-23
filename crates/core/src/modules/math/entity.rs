//! Pure domain entity for math calculation history.

/// Recorded addition operation.
///
/// # Examples
///
/// ```
/// use skills_core::modules::math::entity::CalculationEntry;
///
/// let entry = CalculationEntry { a: 1, b: 2, sum: 3 };
/// assert_eq!(entry, entry);
/// ```
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct CalculationEntry {
    /// Left addend.
    pub a: i64,
    /// Right addend.
    pub b: i64,
    /// Resulting sum.
    pub sum: i64,
}
