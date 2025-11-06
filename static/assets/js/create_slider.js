function create_slider(item){
           var  class1 = 'slider-experts-' + item[0];
           var class2 = 'slider-results-' + item[2];
            $('#results').append('<div class="card custom-card-color feedback-card" >\n' +
                                    '<div class="row">\n' +
                '                        <div class="col col s12 l6"><p><strong>Option</strong></p>\n<p>' + item[4] + '</p></div>\n' +
                '                        <div class="col col s12 l6"><p><strong>Explanation</strong></p>\n' + '<p>' + item[5] + '</p></div>\n' +
                '                    </div>\n' +
                '                    <div class="expert-comp">\n' +
                '                       <div class="row">\n' +
                '                            <div class="col s12">\n<p>Reference assessment</p>\n' +
                '                                    <div class="' + class1 + '"></div>\n' +
                '                           </div>\n' +
                '                       </div>\n' +
                '                       <div class="row valign-wrapper">\n' +
                '                           <div class="col s12">\n<p>Your response</p>\n' +
                '                                <div class="' + class2 + '"></div>\n' +
                '                           </div>\n' +
                '                       </div>\n' +
                '                    </div>\n' +
                '                  </div>');
            $('.' + class1).attr('id', item[0]);
            $('.' + class2).attr('id', item[2]);
            var s1 = document.getElementById(item[0]);
            var s2 = document.getElementById(item[2]);



        noUiSlider.create(s1, {
            start: item[1],
            connect: true,
            step: 0.1,
            orientation: 'horizontal',
            behaviour: "fixed",

            range: {
                'min': 0,
                'max': 5
            },
            format: wNumb({
                decimals: 1
            })
        });

        noUiSlider.create(s2, {
            start: item[3],
            connect: true,
            step: 0.1,
            orientation: 'horizontal',


            range: {
                'min': 0,
                'max': 5
            },
            // pips: {
            //     mode: 'range',
            //     density: 20
            // },
            format: wNumb({
                decimals: 1
            })
        });
        s2.setAttribute('disabled', true);
        var dot = $('[class*="slider-experts"] .noUi-origin');
    dot.addClass('noUi-origin2');
    dot.removeClass('noUi-origin');
}