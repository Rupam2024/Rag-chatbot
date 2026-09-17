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
        generated_time = Paragraph(
            f"Generated On: {datetime.now()}",
            self.styles["Normal"]
        )

        elements.append(
            generated_time
        )

        elements.append(
            Spacer(1, 20)
        )

        for key, value in drug_data.items():

            text = (
                f"<b>{key}</b>: {value}"
            )

            elements.append(
                Paragraph(
                    text,
                    self.styles["BodyText"]
                )
            )

            elements.append(
                Spacer(1, 6)
            )

        doc.build(elements)

        return output_file
