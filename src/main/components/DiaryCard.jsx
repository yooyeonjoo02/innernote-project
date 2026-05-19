function DiaryCard({ content, setContent, isEditMode }) {
  return (
    <section className="diary-card">
      {isEditMode ? (
        <textarea
          className="diary-textarea"
          value={content}
          onChange={(e) => setContent(e.target.value)}
        />
      ) : (
        <p className="diary-content">{content}</p>
      )}
    </section>
  );
}

export default DiaryCard;