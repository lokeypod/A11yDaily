import hashlib
import html
import re

from app.ingestion.normalized_document import NormalizedDocument
from app.ingestion.normalizer import DocumentNormalizer
from app.ingestion.raw_document import RawDocument


class HtmlDocumentNormalizer(DocumentNormalizer):
    """Normalize simple HTML-like source content into plain text."""

    def normalize(self, document: RawDocument) -> NormalizedDocument:
        plain_text = self._extract_plain_text(document.raw_content)
        content_hash = self._create_content_hash(plain_text)

        return NormalizedDocument(
            source_identifier=document.source_identifier,
            external_identifier=document.external_identifier,
            title=document.title.strip(),
            canonical_url=document.url,
            plain_text=plain_text,
            retrieved_at=document.retrieved_at,
            published_at=document.published_at,
            source_summary=document.source_summary,
            author=document.author,
            language=document.language,
            content_hash=content_hash,
            metadata=document.metadata.copy(),
        )

    @staticmethod
    def _extract_plain_text(raw_content: str | None) -> str:
        if not raw_content:
            return ""

        without_tags = re.sub(r"<[^>]+>", " ", raw_content)
        decoded = html.unescape(without_tags)

        return " ".join(decoded.split())

    @staticmethod
    def _create_content_hash(content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()
