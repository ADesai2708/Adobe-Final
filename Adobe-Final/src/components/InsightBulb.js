import React from "react";

export default function InsightBulb({ insights }) {
  if (!insights) return null;

  const Block = ({ title, items }) =>
    items?.length ? (
      <div className="card">
        <h4>{title}</h4>
        <ul>
          {items.map((x, i) => (
            <li key={i}>{x}</li>
          ))}
        </ul>
      </div>
    ) : null;

  return (
    <>
      <Block title="Takeaways" items={insights.takeaways} />
      <Block title="Contradictions" items={insights.contradictions} />
      <Block title="Examples" items={insights.examples} />
      <Block title="Did you know?" items={insights.did_you_know} />
    </>
  );
}
