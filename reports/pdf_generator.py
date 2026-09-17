from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib import colors

from datetime import datetime
import os

# PDF Generator

class PDFGenerator:

    def __init__(self):

        self.styles = getSampleStyleSheet()

    # Create Single Drug Report
    

    def create_drug_report(
        self,
        drug_data,
        output_file
    ):

        doc = SimpleDocTemplate(
            output_file
        )

        elements = []

        title = Paragraph(
            "Drug Information Report",
            self.styles["Title"]
        )

        elements.append(title)

        elements.append(
            Spacer(1, 12)
        )
