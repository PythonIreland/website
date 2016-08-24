
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
          label: 'Click to tweet',
          icon: 'fa fa-twitter',
          command: null
        });
        toolbar.append(button);
        return button.on("click", function(event) {
          var insertionPoint, lastSelection;

          lastSelection = widget.options.editable.getSelection();
          insertionPoint = $(lastSelection.endContainer).parentsUntil('.richtext').last();
                    var quoted = "“" + lastSelection + "”";
                    var escaped = $("<div>").text(quoted).html();
                    var link_ref = "https://twitter.com/share?text="+escaped+"&amp;url=https://www.python.ie/"
                    var link = $("<a>").attr({
                        "target": '_blank',
                        "href": link_ref,
                        }).text(quoted);
                    var elem = $("<blockquote>").attr({
                        "class" : 'tm-click-to-tweet',
                        }).append(link);

                    var tweet = $("<p>").attr({"class" : 'tm-ctt-tip'}).append(
                        link.clone().attr({"class": 'tm-ctt-btn'}).text('Click to tweet'));

                    elem.append(tweet);
                    var node = lastSelection.createContextualFragment($('<div>').append(elem).html());

                    lastSelection.deleteContents();
                    lastSelection.insertNode(node);

                    return widget.options.editable.element.trigger('change');
        });
      }
    });
  })(jQuery);

}).call(this);
