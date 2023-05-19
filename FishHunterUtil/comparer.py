from FishHunterUtil.similarity import calculate_dict_similarity, lcs, ngram_similarity, cosine_similarity, calculate_by_lcs
from datetime import datetime

class Comparer:
    def __init__(self) -> None:
        self.MINIMUM_SCORE = None
        self.MULTIPLIER_CSS = None
        self.MULTIPLIER_HTML = None
        self.MULTIPLIER_TEXT = None

    def calculate_css(self, css1, css2):
        start_time = datetime.now()
        css_score = calculate_dict_similarity(css1, css2)
        end_time = datetime.now()
        total_seconds = (end_time - start_time).total_seconds()

        return css_score, total_seconds

    def calculate_html(self, html1, html2):
        start_time = datetime.now()
        lcs_res = lcs(html1, html2)
        html_score = (2 * lcs_res[0]) / (len(html1) + len(html2))
        end_time = datetime.now()
        total_seconds = (end_time - start_time).total_seconds()
        
        return html_score, total_seconds

    def calculate_text(self, text1, text2):
        start_time = datetime.now()
        # by n-gram, n = 1
        ngram_score = ngram_similarity(text1, text2, 1)

        # by cosine
        cosine_score = cosine_similarity(text1, text2)

        end_time = datetime.now()
        total_seconds = (end_time - start_time).total_seconds()

        return max(ngram_score, cosine_score), total_seconds

    def compare_by_css(self, css1, css2):
        return self.calculate_css(css1, css2)

    def compare_by_html(self, html1, html2):
        return self.calculate_html(html1, html2)

    def compare_by_text(self, text1, text2):
        return self.calculate_text(text1, text2)

    def compare_by_all(self, feature1, feature2):
        css_score, css_time = self.calculate_css(feature1['css'], feature2['css'])
        html_score, html_time = self.calculate_html(feature1['html'], feature2['html'])
        text_score, text_time = self.calculate_text(feature1['text'], feature2['text'])

        total_seconds = css_time + html_time + text_time
        final_score = css_score * self.MULTIPLIER_CSS + html_score * self.MULTIPLIER_HTML + text_score * self.MULTIPLIER_TEXT
        return final_score, total_seconds
