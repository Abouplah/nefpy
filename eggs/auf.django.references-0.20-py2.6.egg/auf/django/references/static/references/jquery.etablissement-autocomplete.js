(function($) {

    function set_ref_etablissement(form, id) {
        form.find('[name=ref]').val(id);
        $.get('/references/etablissements/' + id + '.json', function(data) {
            for (field in data) {
                if (field != 'id') {
                    var widget = form.find('[name=' + field + ']');
                    var value = $('<span class="etablissement-value"></span>');
                    value.insertBefore(widget);
                    if (widget.is(':checkbox')) {
                        value.append('<img src="/static/references/icon-' +
                                     (data[field] ? 'yes' : 'no') + '.gif" alt="' +
                                     (data[field] ? 'oui' : 'non') + '/>');
                        widget.attr('checked', data[field]);
                    }
                    else {
                        value.insertBefore(widget);
                        if (widget.is('select')) {
                            value.append(widget.find('option[value=' + data[field] + ']').text());
                        }
                        else {
                            value.append(data[field]);
                        }
                        widget.val(data[field]);
                    }

                    if (field == 'nom') {
                        var button = $(
                            '<button type="button" class="etablissement-change-button">' +
                            'Modifier</button>'
                        );
                        value.append(' ');
                        button.appendTo(value);
                        button.click(function() { unset_ref_etablissement(form); })
                    }
                    widget.addClass('etablissement-hidden').hide();
                    widget
                        .next('.add-another,.datetimeshortcuts')
                        .addClass('etablissement-hidden')
                        .hide();
                }
            }
        });
    }

    function unset_ref_etablissement(form) {
        form.find('[name=ref]').val('');
        form.find('[name=nom]').val('');
        form.find('.etablissement-value').remove();
        form.find('.etablissement-hidden').show();
    }

    $.fn.etablissement_autocomplete = function(exclude_refs) {

        var form = this.closest('form');

        // Cacher le champ ref et son label
        var ref_field = form.find('[name=ref]');
        ref_field.hide();
        var ref_field_id = ref_field.attr('id');
        if (ref_field_id) {
            form.find('label[for=' + ref_field_id + ']').hide();
        }

        // On vérifie si le champ pays se trouve avant le champ à auto-compléter.
        // Si c'est le cas, on va filtrer l'auto-complétion avec le pays
        // sélectionné.
        var all_inputs = form.find(':input');
        var pays_input = all_inputs.filter('[name=pays]');
        var pays_index = all_inputs.index(pays_input);
        var my_index = all_inputs.index(this);
        var critere_pays = false;
        if (pays_index != -1 && pays_index < my_index) {
            var critere_pays = pays_input.get();
        }

        // Pré-remplir les champs si une référence est déjà indiquée
        var ref_id = form.find('[name=ref]').val();
        if (ref_id) {
            set_ref_etablissement(form, ref_id);
        }

        // Mettre en place l'autocomplete
        this.autocomplete({
            source: function(request, response) {
                if (critere_pays) {
                    request.pays = $(critere_pays).val();
                }
                if (exclude_refs) {
                    request.exclude_refs = exclude_refs;
                }
                if (ref_id) {
                    request.include = ref_id;
                }
                $.getJSON('/references/autocomplete/etablissements.json', request, response);
            },
            select: function(event, ui) {
                set_ref_etablissement(form, ui.item.id)
            }
        });

    }

})(jQuery);
