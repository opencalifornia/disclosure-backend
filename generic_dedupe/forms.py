from django import forms

from .models import DedupeMixin


class DedupeForm(forms.ModelForm):
    """Adds a dropdown for the 'true model'."""
    true_model = forms.ModelChoiceField(queryset=None, required=False)

    def __init__(self, *args, **kwargs):
        super(DedupeForm, self).__init__(*args, **kwargs)
        # Available values are of the same class as the model this form
        # is registered to.
        #
        # Use filtered_objects to limit values only to non-deduped values.
        self.fields['true_model'].queryset = self.Meta.model.filtered_objects.all()
        if 'instance' in kwargs:
            # If there's an instance, set the default value to
            # the current value of that model's "true model ID"
            instance = kwargs['instance']
            true_model_id = instance.true_model_id
            if true_model_id is not None:
                self.fields['true_model'].initial = true_model_id

    def save(self, commit=True):
        """Set the result onto the model."""
        model = super(DedupeForm, self).save(commit=False)
        true_model = self.cleaned_data.get('true_model', None)
        model.true_model_id = getattr(true_model, 'id', None)
        return model

    class Meta:
        model = DedupeMixin
        fields = '__all__'
        exclude = ('true_model_id',)  # Don't show the raw integer field.
