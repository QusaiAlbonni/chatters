<template>
  <v-form @submit.prevent="login()" ref="form">
    <v-container class="fill-height">
      <v-row justify="center">
        <v-col cols="12" md="6">
          <v-card class="px-5 py-5">
            <!--logo-->
            <v-row justify="center" class="">
              <v-col class="text-center pb-0">
                <v-avatar image="../assets/logo.svg" size="75" />
              </v-col>
            </v-row>

            <!--info-->
            <v-row justify="center">
              <v-col class="text-center mb-5">
                <strong>CHATTERS</strong>
              </v-col>
            </v-row>

            <!--Username Field-->
            <v-text-field v-model="username" variant="outlined" rounded="6" label="Username" required></v-text-field>

            <!--Passowrd-->
            <v-text-field :autofocus="false" ref="passwordField" v-model="password"
              :type="passwordVisible ? 'text' : 'password'"
              :append-inner-icon="passwordVisible ? 'mdi-eye' : 'mdi-eye-off'" variant="outlined" clearable rounded="6"
              label="Password" @click:append-inner="togglePasswordVisibility" required></v-text-field>

            <!--checkbox-->
            <v-checkbox v-model="terms" color="secondary" label="I agree to site terms and conditions"></v-checkbox>

            <div class="mx-2"><span>
                <a href="/signup" class="text-caption" style="text-decoration: none;">Don't have an account? Sign-Up</a>
              </span></div>

            <!--Submit-->
            <v-btn class="ml-2" type="submit" :disabled="!enabledButton" color="primary">
              Login
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
import { useTransStore } from '@/stores/translation';

const authStore = useAuthStore()
const appStore = useAppStore()
const router = useRouter()
const transStore = useTransStore()

const username = ref('')
const password = ref('')
const form = ref(null)
const enabledButton = ref(true)

const passwordVisible = ref(false)
const passwordField = ref(null)

const terms = ref(false)

async function login() {
  if (!terms.value) {
    appStore.errorSnackBar.message = "please agree to the terms of use"
    appStore.errorSnackBar.visible = !appStore.errorSnackBar.visible;
    return;
  }
  try {
    enabledButton.value = false;
    await authStore.fetchAuthToken(username.value, password.value);
    await transStore.loadLangs();
    router.push('/chat');
  }
  catch (error) {
    console.log(error);
    appStore.errorSnackBar.message = "Incorrect credentials";
    appStore.errorSnackBar.visible = !appStore.errorSnackBar.visible;
  }
  finally {
    enabledButton.value = true;
  }

}

function togglePasswordVisibility() {
  passwordVisible.value = !passwordVisible.value;
}
</script>
