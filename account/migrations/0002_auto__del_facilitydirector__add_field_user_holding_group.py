# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'FacilityDirector'
        db.delete_table(u'account_facilitydirector')

        # Adding field 'User.holding_group'
        db.add_column(u'account_user', 'holding_group',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='owners', null=True, to=orm['account.HoldingGroup']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'FacilityDirector'
        db.create_table(u'account_facilitydirector', (
            ('holding_group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='owners', to=orm['account.HoldingGroup'])),
            (u'user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['account.User'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'account', ['FacilityDirector'])

        # Deleting field 'User.holding_group'
        db.delete_column(u'account_user', 'holding_group_id')


    models = {
        u'account.holdinggroup': {
            'Meta': {'object_name': 'HoldingGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'account.user': {
            'Meta': {'object_name': 'User'},
            'budget': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'care_bathing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'care_combinative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'care_current': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'care_diabetic': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'care_diagnosed_memory': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'care_medical_assistance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'care_memory_issues': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'care_mobility': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'care_toileting': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'care_wandering': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'desired_city': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            'health_description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'holding_group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owners'", 'null': 'True', 'to': u"orm['account.HoldingGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'move_in_time_frame': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'pay_longterm_care': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pay_medicaid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pay_medicare': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pay_private_pay': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pay_ssi': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pay_veterans_benefits': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'planned_move_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'resident_first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'searching_for': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['account']