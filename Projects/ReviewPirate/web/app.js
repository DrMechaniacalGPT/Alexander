const state = {
  data: null,
  answers: {},
};

const els = {
  title: document.querySelector("#title"),
  questions: document.querySelector("#questions"),
  fit: document.querySelector("#fit"),
  evidence: document.querySelector("#evidence"),
  sources: document.querySelector("#sources"),
  filter: document.querySelector("#product-filter"),
  reset: document.querySelector("#reset"),
  questionTemplate: document.querySelector("#question-template"),
};

function productName(id) {
  const product = state.data.products.find((item) => item.id === id);
  return product ? product.name : id;
}

function sourceById(id) {
  return state.data.sources.find((item) => item.id === id);
}

function renderQuestions() {
  els.questions.innerHTML = "";

  for (const question of state.data.decision_questions || []) {
    const node = els.questionTemplate.content.cloneNode(true);
    const input = node.querySelector("input");
    const text = node.querySelector(".question-text");

    input.checked = Boolean(state.answers[question.id]);
    input.dataset.questionId = question.id;
    text.textContent = question.prompt;

    input.addEventListener("change", (event) => {
      state.answers[question.id] = event.target.checked;
      renderFit();
    });

    els.questions.appendChild(node);
  }
}

function matchingOutcomes() {
  const matches = [];

  for (const question of state.data.decision_questions || []) {
    const answer = Boolean(state.answers[question.id]);

    for (const outcome of question.outcomes || []) {
      if (outcome.answer === answer && answer === true) {
        matches.push({
          question: question.prompt,
          productId: outcome.product_id,
          reason: outcome.reason,
        });
      }
    }
  }

  return matches;
}

function renderFit() {
  const matches = matchingOutcomes();
  els.fit.innerHTML = "";

  if (!matches.length) {
    els.fit.innerHTML = '<p class="muted">No current decision rule fires. Keep reading the evidence.</p>';
    return;
  }

  for (const match of matches) {
    const card = document.createElement("div");
    card.className = "fit-card";

    const title = document.createElement("strong");
    title.textContent = productName(match.productId);

    const reason = document.createElement("div");
    reason.textContent = match.reason;

    const because = document.createElement("div");
    because.className = "claim-meta";
    because.textContent = "because: " + match.question;

    card.append(title, reason, because);
    els.fit.appendChild(card);
  }
}

function groupedClaims(productId) {
  const result = new Map();

  for (const claim of state.data.claims || []) {
    if (claim.product_id !== productId) continue;
    if (!result.has(claim.topic)) result.set(claim.topic, []);
    result.get(claim.topic).push(claim);
  }

  return result;
}

function renderEvidence() {
  els.evidence.innerHTML = "";
  const filter = els.filter.value;

  for (const product of state.data.products) {
    if (filter !== "all" && filter !== product.id) continue;

    const section = document.createElement("section");
    section.className = "evidence-product";

    const heading = document.createElement("h3");
    heading.textContent = product.name;
    section.appendChild(heading);

    const topics = groupedClaims(product.id);

    for (const [topicName, claims] of [...topics.entries()].sort()) {
      const topic = document.createElement("div");
      topic.className = "topic";

      const h4 = document.createElement("h4");
      h4.textContent = topicName;
      topic.appendChild(h4);

      const counts = {
        support: claims.filter((claim) => claim.stance === "support").length,
        oppose: claims.filter((claim) => claim.stance === "oppose").length,
        qualify: claims.filter((claim) => claim.stance === "qualify").length,
      };

      const signalRow = document.createElement("div");
      signalRow.className = "signal-row";

      for (const [label, count] of Object.entries(counts)) {
        if (!count) continue;
        const badge = document.createElement("span");
        badge.className = "signal";
        badge.textContent = label + ": " + count;
        signalRow.appendChild(badge);
      }

      topic.appendChild(signalRow);

      for (const claim of claims) {
        const source = sourceById(claim.source_id);
        const item = document.createElement("div");
        item.className = "claim";

        const text = document.createElement("div");
        text.textContent = claim.claim;

        const meta = document.createElement("div");
        meta.className = "claim-meta";

        const confidence = claim.confidence == null
          ? "confidence unknown"
          : "confidence " + Math.round(claim.confidence * 100) + "%";

        meta.append(
          document.createTextNode(
            [claim.evidence_type, confidence, claim.stance].filter(Boolean).join(" · ") + " · "
          )
        );

        if (source) {
          const link = document.createElement("a");
          link.href = source.url;
          link.target = "_blank";
          link.rel = "noreferrer";
          link.textContent = source.title;
          meta.appendChild(link);
        }

        item.append(text, meta);

        if (claim.note) {
          const note = document.createElement("div");
          note.className = "claim-meta";
          note.textContent = claim.note;
          item.appendChild(note);
        }

        topic.appendChild(item);
      }

      section.appendChild(topic);
    }

    els.evidence.appendChild(section);
  }
}

function renderSources() {
  els.sources.innerHTML = "";

  for (const source of state.data.sources || []) {
    const item = document.createElement("div");
    item.className = "source";

    const link = document.createElement("a");
    link.href = source.url;
    link.target = "_blank";
    link.rel = "noreferrer";
    link.textContent = source.title;

    const meta = document.createElement("div");
    meta.className = "source-meta";
    meta.textContent = [
      source.kind,
      "first hand: " + String(source.first_hand ?? "unknown"),
      "financial relationship: " + String(source.financial_relationship ?? "unknown"),
    ].join(" · ");

    item.append(link, meta);
    els.sources.appendChild(item);
  }
}

function renderFilter() {
  for (const product of state.data.products) {
    const option = document.createElement("option");
    option.value = product.id;
    option.textContent = product.name;
    els.filter.appendChild(option);
  }

  els.filter.addEventListener("change", renderEvidence);
}

els.reset.addEventListener("click", () => {
  state.answers = {};
  renderQuestions();
  renderFit();
});

async function main() {
  const response = await fetch("../data/mlm2pro-vs-square.json");
  if (!response.ok) throw new Error("could not load comparison data");

  state.data = await response.json();
  els.title.textContent = state.data.comparison;

  renderQuestions();
  renderFit();
  renderFilter();
  renderEvidence();
  renderSources();
}

main().catch((error) => {
  els.title.textContent = "Review Pirate ran aground";
  els.fit.innerHTML = '<p class="muted"></p>';
  els.fit.querySelector("p").textContent = error.message;
});
