export const getChangedDate = (
  selectedDate,
  viewType,
  amount
) => {
  const current = new Date(selectedDate);

  if (viewType === 'daily') {
    current.setDate(current.getDate() + amount);
  }

  if (viewType === 'weekly') {
    current.setDate(current.getDate() + amount * 7);
  }

  if (viewType === 'monthly') {
    current.setMonth(current.getMonth() + amount);
  }

  const year = current.getFullYear();
  const month = String(current.getMonth() + 1).padStart(2, '0');
  const day = String(current.getDate()).padStart(2, '0');

  return `${year}-${month}-${day}`;
};