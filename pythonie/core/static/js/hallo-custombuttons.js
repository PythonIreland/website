
(function() {
  (function($) {
    return $.widget("IKS.clicktotweet", {
      options: {
        uuid: '',
        editable: null
      },
      populateToolbar: function(toolbar) {
        var button, widget;

        widget = this;
        button = $('<span></span>');
        button.hallobutton({
          uuid: this.options.uuid,
          editable: this.options.editable,
          label: 'Pull Out Quote',
          icon: 'fa fa-twitter',
          command: null
        });
        toolbar.append(button);
        return button.on("click", function(event) {
          var insertionPoint, lastSelection;

          lastSelection = widget.options.editable.getSelection();
          insertionPoint = $(lastSelection.endContainer).parentsUntil('.richtext').last();
                    var elem;

//                    elem = "<div class='tm-tweet-clear'></div>";
//                    elem = "<div class='tm-click-to-tweet'>dfsdfsdfs</div>";
//                    elem = elem + "<div class='tm-click-to-tweet'> \
//                                    "<div class='tm-ctt-text'>"\
//                                    "<a href='https://twitter.com/share?text=%22Let.%22&amp;url=https://blog/'"\
//                                       "arget='_blank'>“Let.”"\
//                                       "</a>"\
//                                       "</div>"\
//                                    "<p><a href='https://twitter.com/share?text=%22Let.%22&amp;url=https://blog/'" \
//                                          "target='_blank' class='tm-ctt-btn'>Click To Tweet</a>" \
//                                    "</p><div class='tm-ctt-tip'></div>" \
//                                    "</div>";
                    elem = "<blockquote class='tm-click-to-tweet'><a target='_blank' href='https://twitter.com/share?text=%22Let.%22&amp;url=https://blog/'>“" + lastSelection + "”</a></blockquote>";
//                    elem = "<blockquote class='tm-click-to-tweet'>“" + lastSelection + "”</blockquote>";

                    var node = lastSelection.createContextualFragment(elem);

                    lastSelection.deleteContents();
                    lastSelection.insertNode(node);

                    return widget.options.editable.element.trigger('change');
        });
      }
    });
  })(jQuery);

}).call(this);
