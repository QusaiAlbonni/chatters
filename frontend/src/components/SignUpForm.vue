<template>
  <v-form @submit.prevent="signup" ref="form">
    <v-container class="fill-height">
      <v-row justify="center">
        <v-col cols="12" md="6">
          <v-card class="px-5 py-5">
            <!--logo-->
            <v-row justify="center" class="">
              <v-col class="text-center pb-0">
                <v-avatar :image="avatarUrl" size="150" />
              </v-col>
            </v-row>

            <!--info-->
            <v-row justify="center">
              <v-col class="text-center mb-5">
                <strong></strong>
              </v-col>
            </v-row>

            <!--Username Field-->
            <v-text-field :rules="[v => !!v || 'username is required']" :error-messages="usernameErrors" v-model="username" variant="outlined" rounded="6" label="Username"
              prepend-icon="mdi-account" required class="my-2"></v-text-field>

            <!--Email Field-->
            <v-text-field :rules="[v => !!v || 'email is required']" type="email" :error-messages="emailErrors" v-model="email" variant="outlined" rounded="6" label="Email"
              prepend-icon="mdi-email" required class="my-2"></v-text-field>

            <!--Passowrd-->
            <v-text-field :error-messages="passwordErrors" :autofocus="false" ref="passwordField" v-model="password"
              :type="passwordVisible ? 'text' : 'password'" :rules="[v => !!v || 'password is required']"
              :append-inner-icon="passwordVisible ? 'mdi-eye' : 'mdi-eye-off'" variant="outlined" clearable rounded="6"
              label="Password" @click:append-inner="togglePasswordVisibility" prepend-icon="mdi-lock" required class="my-2"></v-text-field>

            <!--Avatar Image-->
            <v-file-input v-model="avatar" :show-size="1000" color="deep-purple-accent-4" label="Your Avatar"
              :rules="[v => !!v || 'avatar is required']"
              placeholder="Select your files" prepend-icon="mdi-paperclip" variant="outlined" required
              class="my-2">
            </v-file-input>

            <!--checkbox-->
            <v-checkbox v-model="terms" color="secondary" label="I agree to site terms and conditions" :rules="[v => !!v || 'you must agree']" required></v-checkbox>

            <!--Submit-->
            <v-btn class="ml-2 mt-5" type="submit" :disabled="!enabledButton" color="primary">
              Sign-up
            </v-btn>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-form>
</template>

<script lang="ts" setup>
import { useAuthStore } from '@/stores/auth';
import { ref } from 'vue';
import { useAppStore } from '@/stores/app';
import { useRouter } from 'vue-router';
import { VForm } from 'vuetify/components';

const authStore = useAuthStore()
const appStore = useAppStore()
const router = useRouter()

const username = ref('')
const password = ref('')
const email: Ref<string> = ref('')
const form: Ref<VForm | null> = ref(null)
const enabledButton = ref(true)

const passwordVisible = ref(false)
const passwordField = ref(null)
const passwordErrors: Ref<string[] | null> = ref(null)

const usernameErrors: Ref<string[] | null> = ref(null)

const emailErrors: Ref<string[] | null> = ref(null)

const terms = ref(false)

const avatar: Ref<File | null> = ref(null)

const avatarUrl: Ref<string> = ref("/logo.svg")

function togglePasswordVisibility() {
  passwordVisible.value = !passwordVisible.value;
}

async function signup(){
  enabledButton.value = false
  try{
    await authStore.createUser(username.value, password.value, avatar.value, email.value)
    router.push('/login')
  }
  catch (error){
    let data = error.response.data;
    usernameErrors.value = data['username'];
    passwordErrors.value = data['password'];
    emailErrors.value = data['email'];
    appStore.errorSnackBar.message = "invalid Form please correct the errors";
    appStore.errorSnackBar.visible = true;

    form.value?.resetValidation();
  }
  finally{
    enabledButton.value = true
  }
}

watch(avatar, () => {
  if (avatar.value)
    avatarUrl.value = URL.createObjectURL(avatar.value);
})
</script>
