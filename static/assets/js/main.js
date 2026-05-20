  /* *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
  /////////////////   Down Load Button Function   /////////////////
  *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** */

  (function ($) {
    'use strict';
  
    $('#tm_download_btn').on('click', function () {
        var downloadSection = $('#tm_download_section');
        var cWidth = downloadSection.width();
        var cHeight = downloadSection.height();
        var topLeftMargin = 0;
        var pdfWidth = cWidth + topLeftMargin * 2;
        var pdfHeight = pdfWidth * 1.5 + topLeftMargin * 2;
  
        html2canvas(downloadSection[0], { allowTaint: true }).then(function (canvas) {
            var pdf = new jsPDF({
                orientation: 'p',
                unit: 'pt',
                format: [pdfWidth, pdfHeight]
            });

            pdf.addImage(canvas.toDataURL('image/png', 1.0), 'PNG', 0, 0, pdfWidth, pdfHeight);
            pdf.save('download.pdf');
        });
    });
})(jQuery);

